from typing import List

import click

from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.pipeline_steps.pipeline_step import PipelineStep


class FilterSites(PipelineStep):
    def run(self, context: PipelineContext) -> PipelineContext:
        is_exclude = context.user_input.exclude is not None
        is_include = context.user_input.exclude is not None

        if is_include and is_exclude:
            raise click.BadParameter(
                f'--include and --exclude are mutually exclusive. Use --include or --exclude to specify the sources to include or exclude.')

        if is_exclude:
            filtered_sites = [site_config for site_config in context.site_configs if site_config.abbreviation not in context.user_input.exclude]
        elif is_include:
            filtered_sites = [site_config for site_config in context.site_configs if site_config.abbreviation in context.user_input.include]
        else:
            filtered_sites = context.site_configs.copy()

        context.site_configs = filtered_sites
        return context
