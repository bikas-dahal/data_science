from crewai import Crew, Process 
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task 

# Create a crew
crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, write_task],
    processes=Process.sequential,
    memory = True,
    cache = True,
    max_rpm = 100,
    share_crew = True
    )

result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
print(result)