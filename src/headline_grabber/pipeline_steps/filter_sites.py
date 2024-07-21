from typing import List
import click
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from tqdm import tqdm


class FilterSites(PipelineStep):
    def run(self, context: PipelineContext) -> PipelineContext:
        if context.user_input.include and context.user_input.exclude:
            raise click.BadParameter(
                f"--include and --exclude are mutually exclusive. Use --include or --exclude to specify the sources to include or exclude."
            )
        if context.user_input.exclude:
            filtered_sites = [
                site_config
                for site_config in tqdm(
                    context.site_configs, desc="FilterSites - Excluding"
                )
                if site_config.abbreviation not in context.user_input.exclude
            ]
        elif context.user_input.include:
            filtered_sites = [
                site_config
                for site_config in tqdm(
                    context.site_configs, desc="FilterSites - Including"
                )
                if site_config.abbreviation in context.user_input.include
            ]
        else:
            filtered_sites = context.site_configs.copy()
        context.site_configs = filtered_sites
        return context
