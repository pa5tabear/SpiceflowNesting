from langchain.agents import initialize_agent, AgentType
from langchain import OpenAI
from scoring import Score
from sqlalchemy.orm import Session
from config import settings
from sqlalchemy import create_engine

engine = create_engine(settings.DATABASE_URL)


def pick_listings():
    db = Session(bind=engine)
    top = (
        db.query(Score)
        .filter(Score.score >= 80)
        .order_by(Score.score.desc())
        .limit(10)
        .all()
    )
    db.close()
    return "\n".join(f"{s.listing_id} – {s.score}" for s in top)


def run_agent():
    llm = OpenAI(temperature=0.2)
    tools = []
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    agent.run(f"User likes high-score rentals. Show today’s picks:\n{pick_listings()}")


if __name__ == "__main__":
    run_agent()
