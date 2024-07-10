from typing import List, Dict
from collections import Counter
from statistics import mean
from tqdm import tqdm
from headline_grabber.models.display_document import DisplayDocument
from headline_grabber.models.headline import Classification
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from headline_grabber.pipeline_steps import (
    text_summarization_tokenizer,
    text_summarization_model,
    headline_tokenizer,
    headline_model,
)


class PrepareForDisplay(PipelineStep):
    def run(self, context: PipelineContext):
        documents_for_display: Dict[str, List[DisplayDocument]] = {}
        for label, headlines in tqdm(context.grouped_headlines.items(), desc="Preparing documents for display", unit="group"):
            links = sorted(list(set([headline.link for headline in headlines])))
            summarized_title = self._generate_headline(
                [
                    " ".join([headline.title, headline.description])
                    for headline in headlines
                ]
            )
            summarized_description = self._summarize_text(
                [
                    " ".join([headline.title, headline.description])
                    for headline in headlines
                ],
                min_length=150,
                max_length=250,
            )
            subjects = sorted(
                list(set([headline.subject.label for headline in headlines]))
            )
            most_common_subject = Counter(
                [headline.subject.label for headline in headlines]
            ).most_common()[0][0]
            most_common_sentiment = Counter(
                [headline.sentiment.label for headline in headlines]
            ).most_common()[0][0]
            average_sentiment_score = round(
                mean(
                    [
                        i.sentiment.score
                        for i in list(
                            filter(
                                lambda x: x.sentiment.label == most_common_sentiment,
                                [headline for headline in headlines],
                            )
                        )
                    ]
                ),
                3,
            )
            display_document = DisplayDocument(
                links=links,
                summarized_title=summarized_title,
                summarized_description=summarized_description,
                average_sentiment=Classification(
                    label=most_common_sentiment, score=average_sentiment_score
                ),
                subjects=subjects,
                most_common_subject=most_common_subject,
            )
            if most_common_subject not in documents_for_display:
                documents_for_display[most_common_subject] = [display_document]
            else:
                documents_for_display[most_common_subject] = documents_for_display[
                    most_common_subject
                ] + [display_document]

        context.documents_for_display = documents_for_display
        return context

    def _summarize_text(
        self, texts: List[str], min_length: int, max_length: int
    ) -> str:
        inputs = text_summarization_tokenizer(
            texts,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
            padding="max_length",
        )
        summary_ids = text_summarization_model.generate(
            inputs["input_ids"],
            num_beams=4,
            length_penalty=2.0,
            max_length=max_length,
            min_length=min_length,
            early_stopping=True,
        )
        summary = text_summarization_tokenizer.decode(
            summary_ids[0], skip_special_tokens=True
        )
        return summary

    def _generate_headline(self, texts: List[str]) -> str:
        text = "headline: " + " ".join(texts)
        encoding = headline_tokenizer.encode_plus(text, return_tensors="pt")
        input_ids = encoding["input_ids"]
        attention_masks = encoding["attention_mask"]
        beam_outputs = headline_model.generate(
            input_ids=input_ids,
            attention_mask=attention_masks,
            max_length=64,
            num_beams=3,
            early_stopping=True,
        )
        result = headline_tokenizer.decode(beam_outputs[0])
        result = result.replace("<pad> ", "").replace("</s>", "")
        return result