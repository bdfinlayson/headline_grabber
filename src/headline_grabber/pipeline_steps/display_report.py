import os
import time
import webbrowser
from datetime import datetime

from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.pipeline_steps.pipeline_step import PipelineStep

import dominate
from dominate.tags import *


class DisplayReport(PipelineStep):
    def run(self, context: PipelineContext):
        doc = dominate.document(title='Dominate your HTML')
        subjects = context.documents_for_display.keys()
        news_sources = [config.name for config in context.site_configs]
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H_%M")
        reports_dir = os.path.join(os.getcwd(), 'reports')
        html_file_path = os.path.join(reports_dir, f"news_report_{formatted_datetime}.html")

        # ensure reports directory exists
        os.makedirs(reports_dir, exist_ok=True)

        with doc.head:
            link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css')
            script(type='text/javascript', src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js')

        with doc:
            with div(cls='container'):
                with div(cls='row'):
                    with div(cls='col-12'):
                        h1('Headline Grabber Report')
                        with div(cls='fst-italic'):
                            p(f'Generated At: {formatted_datetime}')
                            p(f'This report contains content from the following news sources: {", ".join(news_sources)}')
                for subject in subjects:
                    with div(cls='row'):
                        h2(subject)
                        for headline in context.documents_for_display[subject]:
                            with div(cls='col-6'):
                                h4(headline.summarized_title)
                                p(headline.summarized_description)
                                with b('Sentiment:'):
                                    span(f'{headline.average_sentiment.label} ({headline.average_sentiment.score})')
                                p(b('Sources:'))
                                with ol():
                                    for lnk in headline.links:
                                        li(a(lnk, href=lnk))
                        hr()

        self._display_report(str(doc), html_file_path)

    def _display_report(self, html_content: str, file_path: str):
        try:
            with open(file_path, "w") as file:
                file.write(html_content)
            print(f"HTML file created at: {file_path}")
        except Exception as e:
            print(f"Failed to write HTML file: {e}")
            exit(1)

        # Open the HTML file in the default web browser
        try:
            print(os.path.realpath(file_path))
            webbrowser.open('file://' + os.path.realpath(file_path))
        except Exception as e:
            print(f"Failed to open HTML file in web browser: {e}")
