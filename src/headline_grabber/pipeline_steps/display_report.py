import os
import webbrowser
from datetime import datetime
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep
import dominate
from dominate.tags import *
from tqdm import tqdm


class DisplayReport(PipelineStep):
    formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H_%M")

    def run(self, context: PipelineContext):
        html_file_path = self.build_html_file_path(context.user_input.target_dir)
        html_content = self.build_html_content(context)
        self._display_report(html_content, html_file_path)

    @staticmethod
    def _display_report(html_content: str, file_path: str) -> bool:
        try:
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(DisplayReport.sanitize_html_content(html_content))
            webbrowser.open("file://" + os.path.realpath(file_path))
            return True
        except Exception as e:
            print(f"Failed to write/open HTML file in web browser: {e}")
            return False

    @staticmethod
    def build_export_path(target_dir: str) -> str:
        if target_dir:
            # ensure reports directory exists
            os.makedirs(target_dir, exist_ok=True)
            return target_dir
        else:
            default_dir = os.path.join(os.getcwd(), "reports")
            os.makedirs(default_dir, exist_ok=True)
            return default_dir

    @staticmethod
    def sanitize_html_content(html_content):
        text = (
            html_content.replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
            .replace("’", "'")
            .replace("—", "-")
        )

        return text

    @staticmethod
    def build_html_file_path(target_dir: str) -> str:
        reports_dir = DisplayReport.build_export_path(target_dir)
        return os.path.join(reports_dir, f"news_report_{DisplayReport.formatted_datetime}.html")

    def build_html_content(self, context: PipelineContext) -> str:
        doc = dominate.document(title="Dominate your HTML")
        subjects = context.documents_for_display.keys()
        news_sources = [config.name for config in context.site_configs]

        with doc.head:
            link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
            )
            script(
                type="text/javascript",
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
            )

        with doc:
            with div(cls="container"):
                with div(cls="row"):
                    with div(cls="col-12"):
                        h1("Headline Grabber Report")
                        with div(cls="fst-italic"):
                            p(f"Generated At: {self.formatted_datetime}")
                            p(
                                f'This report contains content from the following news sources: {", ".join(news_sources)}'
                            )
                with div(cls="accordion", id="accordionExample"):
                    for idx, subject in enumerate(tqdm(subjects, desc="Generating report")):
                        with div(cls="accordion-item"):
                            with h2(cls="accordion-header", id=f"heading{idx}"):
                                button(
                                    subject,
                                    cls="accordion-button",
                                    type="button",
                                    data_bs_toggle="collapse",
                                    data_bs_target=f"#collapse{idx}",
                                    aria_expanded= "true" if idx==0 else "false",
                                    aria_controls=f"collapse{idx}"
                                )
                            with div(
                                cls=f"accordion-collapse collapse{' show' if idx==0 else ''}",
                                id=f"collapse{idx}",
                                aria_labelledby=f"heading{idx}",
                                data_bs_parent="#accordionExample"
                            ):
                                with div(cls="accordion-body"):
                                    for headline in context.documents_for_display[subject]:
                                        with div(cls="col-6"):
                                            h4(headline.summarized_title)
                                            p(headline.summarized_description)
                                            with b("Sentiment:"):
                                                span(
                                                    f"{headline.average_sentiment.label} ({headline.average_sentiment.score})"
                                                    )
                                            p(b("Sources:"))
                                            with ol():
                                                for lnk in headline.links:
                                                    li(a(lnk, href=lnk))
                                    hr()
        return str(doc)
