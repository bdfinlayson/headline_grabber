from transformers import pipeline
from tqdm import tqdm
from headline_grabber.models.headline import Classification
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps import (
    subject_classification_model,
    subject_classification_tokenizer,
)
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep


class ClassifySubject(PipelineStep):
    # the model's subject classes are listed here: https://paperswithcode.com/dataset/ag-news
    subject_class_label_mapping = {
        "LABEL_0": "World",
        "LABEL_1": "Sports",
        "LABEL_2": "Business",
        "LABEL_3": "Science/Technology",
        "LABEL_4": "Politics",
    }

    def run(self, context: PipelineContext):
        classifier = pipeline(
            "text-classification",
            model=subject_classification_model,
            tokenizer=subject_classification_tokenizer,
        )
        texts = [
            " ".join([headline.title, headline.description])
            for headline in context.headlines
        ]
        results = classifier(texts)
        context.headlines = [
            headline.set_subject_classification(
                Classification(
                    self.subject_class_label_mapping[result["label"]], result["score"]
                )
            )
            
            for headline, result in tqdm(zip(context.headlines, results), desc="Classifying subjects", unit="headline", total=len(context.headlines))
               
        ]
        return context
