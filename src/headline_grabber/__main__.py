import click

from headline_grabber.configurations.sites import sites
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences
from headline_grabber.pipelines import news_pipeline
from headline_grabber.validators.click.validate_site_name import validate_site_name


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.option(
    "--include",
    "-i",
    type=click.STRING,
    default=None,
    required=False,
    callback=validate_site_name,
    help="Comma-separated list of news sources to include in the search",
)
@click.option(
    "--exclude",
    "-e",
    type=click.STRING,
    default=None,
    required=False,
    callback=validate_site_name,
    help="Comma-separated list of news sources to exclude from the search",
)
def main(include: str, exclude: str):
    """Simple program to collect headlines from various news sources and summarize them in a helpful way"""
    pipeline_context = PipelineContext(
        site_configs=sites,
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=(include.split(",") if include else None),
            exclude=(exclude.split(",") if exclude else None),
        ),
    )
    pipeline_context = news_pipeline.run(pipeline_context)
    print(pipeline_context)
