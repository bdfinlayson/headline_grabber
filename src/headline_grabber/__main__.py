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
def main(include: str, exclude: str, target_dir: str):
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
        ),
    )
    pipeline_context = news_pipeline.run(pipeline_context)

