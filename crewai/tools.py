from crewai_tools import YoutubeChannelSearchTool
import os
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "key"

yt_tool = SerperDevTool()