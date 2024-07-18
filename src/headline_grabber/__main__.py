import click

from headline_grabber.configurations.sites import sites
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences
from headline_grabber.pipelines import news_pipeline
from headline_grabber.validators.click.option_validator import OptionValidator


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
    callback=OptionValidator.validate_site_name,
    help="Comma-separated list of news sources to include in the search",
)
@click.option(
    "--exclude",
    "-e",
    type=click.STRING,
    default=None,
    required=False,
    callback=OptionValidator.validate_site_name,
    help="Comma-separated list of news sources to exclude from the search",
)
@click.option(
    "--target-dir",
    "-td",
    type=click.STRING,
    default=None,
    required=False,
    callback=OptionValidator.validate_target_dir,
    help="The target directory where html news reports should be exported to",
)
@click.option(
    "--limit",
    "-l",
    type=str,
    default=None,
    required=False,
    callback=OptionValidator.validate_max_entries,
    help="Number specifying the maximum number of entries per topic in a report",
)
@click.option(
    "--filter-sentiment",
    "-f",
    type=str,
    default=None,
    required=False,
    callback=OptionValidator.validate_filter_sentiment,
    help="Filters out news headlines ranked positive or negative based on entered value of positive or negative",
)
def main(include: str, exclude: str, target_dir: str, limit: int, filter_sentiment: str):
    """Simple program to collect headlines from various news sources and summarize them in a helpful way"""
    pipeline_context = PipelineContext(
        site_configs=sites,
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=(include.split(",") if include else None),
            exclude=(exclude.split(",") if exclude else None),
            target_dir=(target_dir if target_dir else None),
            limit=(limit if limit else None),
            filter_sentiment=(filter_sentiment if filter_sentiment else None),
        ),
    )
    pipeline_context = news_pipeline.run(pipeline_context)

