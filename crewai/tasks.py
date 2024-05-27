from crewai import Task 
from tools import yt_tool
from agents import blog_researcher, blog_writer


# Research task 

research_task = Task(
    description=(
        "Research the topic {topic} and provide relevant content for the blog post."
    ),
    expected_output='Professional blog content with proper quotes and source',
    tools=yt_tool,
    agent=[blog_researcher],
    )

# Write task

write_task = Task(
    description=(
        "Write a professional blog post on the topic {topic}."
    ),
    expected_output='Professional blog post with proper quotes and source',
    tools=yt_tool,
    agent=[blog_writer],
    async_execution =False,
    output_files = 'new_blog_post.md'
    )