from src.headline_grabber.models.headline import Classification
from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.pipeline_steps import text_similarity_model
from src.headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from sklearn.cluster import AgglomerativeClustering
import numpy as np


class TextSimilarity(PipelineStep):
    # hyperparameter that limits the distance one document can be from another to be marked as sharing the same subject
    threshold = 0.4

    def run(self, context: PipelineContext):
        texts = [' '.join([headline.title, headline.description]) for headline in context.headlines]
        embeddings = text_similarity_model.encode(texts)

        # first calculate the similarities between the texts
        # under the hood, this method computes the cosine similarity
        # looks like: np.array([[1.0, 0.4, 0.8], [0.2, 1.0, 0.5], [0.9, 0.3, 1.0]])
        similarity_matrix = text_similarity_model.similarity(embeddings, embeddings)

        # then use the similarity matrix numbers to discover which texts are likely about the same topic
        clustering = AgglomerativeClustering(
            n_clusters=None,
            linkage='average',
            distance_threshold=1 - self.threshold
        )

        clustering.fit(1 - similarity_matrix)
        similarity_groups = clustering.labels_

        context.headlines = [headline.set_similarity_classification(similarity_group, similarity_scores) for headline, similarity_group, similarity_scores in zip(context.headlines, similarity_groups, similarity_matrix)]

        return context


