# Sprint 2 
Ryan McFarland, OrionSkywalker, HeadlineGrabber
### What you planned to do
* HG7 - Define a new command line option to specify the desired topics for headlines (only 4 specific topics)
* HG23 - Add configuration for parsing of HTML data from NPR (National Public Radio)
* HG25 - Add configuration for parsing of HTML data from APN (AP News)
### What you did not do
* HG7 - Define a new command line option to specify the desired topics for headlines (only 4 specific topics)
### What problems you encountered
* General inexperience
* Unplanned scheduling conflict
### Issues you worked on
* https://github.com/bdfinlayson/headline_grabber/commit/0738fc0643e46546d30383b76762665cf9333d6c
* https://github.com/bdfinlayson/headline_grabber/commit/165db2292c9dd831074d55b503bc49152cb2ba4a
### Files you worked on
* src/headline_grabber/__main__.py
* src/headline_grabber/models/user_preferences.py
* src/headline_grabber/pipeline_steps/filter_topic.py
* src/headline_grabber/pipelines/__init__.py
* src/headline_grabber/validators/click/option_validator.py
* src/headline_grabber/configurations/sites/npr.yaml
* src/headline_grabber/configurations/sites/apn.yaml
### What you accomplished
* I added configuration files to support scraping data from Associated Press and National Public Radio websites.
* I worked on supporting filtering news by topic, which is incomplete as of this date.
