import click

from src.headline_grabber.configurations.sites import sites
from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.models.user_preferences import UserPreferences
from src.headline_grabber.pipelines import news_pipeline
from src.headline_grabber.validators.click.validate_site_name import validate_site_name, validate_max_entries


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
@click.option(
    "--limit",
    "-l",
    type=str,
    default=None,
    required=False,
    callback=validate_max_entries,
    help="Number specifying the maximum number of entries per topic in a report",
)
def main(include: str, exclude: str, limit: int):
    """Simple program to collect headlines from various news sources and summarize them in a helpful way"""
    pipeline_context = PipelineContext(
        site_configs=sites,
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=(include.split(",") if include else None),
            exclude=(exclude.split(",") if exclude else None),
            limit=(limit if limit else None),
        ),
    )
    pipeline_context = news_pipeline.run(pipeline_context)
    print(pipeline_context)
