from crewai_tools import YoutubeChannelSearchTool
import os
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "34210352cdc15566cdb255f37206de4db4c5e226f97b7fc96910b8eadcaefe97"

yt_tool = SerperDevTool()