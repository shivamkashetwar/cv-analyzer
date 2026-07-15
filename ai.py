from openai import OpenAI
import json

client = OpenAI()

def analyze_resume(resume_text,user_goal):
    prompt = f"""
       you are a senior sofware engineer and hiring manager.

       evatuate the resume base on the user goal .
       user goal : "{user_goal}"

      STRICT RULES:
      - Extractonly relevant skills for this goal
      - REMOVE any irrelevant tool [excel for backend , etc.]
      -Idemtify the real gaps
      -Generate the roadmap only for missing fields
      -make output DIFFERENT base on gole

      return only json:
      {{
      "skills":[],
      "missing_skills":[],
      "roasmap":[],
      "interview_questions":[],

      }}
      Resume:
      {resume_text}

    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.3,
             messages=[{"role": "system", "content": "you are stricts hiring manager."},
                       {"role": "user", "content": prompt}]

        )

        content = response.choices[0].message.content.strip()

        start = content.find("{")
        end = content.rfind("}")+1
        return json.loads(content[start:end])
    
    except Exception as e:
        return{
            "skills":[],
            "missing_skills":[],
            "roadmap":[],
            "interview_questions":[],
            "error": str(e)
        }