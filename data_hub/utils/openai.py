from dotenv import load_dotenv
import os
import openai
import json
from data_hub.utils.database_ops import PreferencesDataOps
from data_hub.utils.filter import DashboardData
from data_hub.models.model import UserPreferences


class AIcall:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")

    def openai_chat_completion(self, system_prompt, user_prompt):
        openai.api_key = self.api_key
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        message = completion["choices"][0]["message"]["content"]
        return message


class Enrichment:
    def __init__(self, user_id: str, company_id: str) -> None:
        self.user_id = user_id
        self.company_id = company_id

    def fetch_preferences(self):
        db = PreferencesDataOps()
        preferences = db.find_document(self.user_id, self.user_id)
        pref_object = json.loads(preferences["preferences"])
        return pref_object

    def fetch_company_details(self):
        rdb = DashboardData(self.user_id)
        company_details = rdb.search_company_id(self.company_id)
        return company_details

    def prompt_creation(self):
        # print(self.fetch_preferences())
        preferences = UserPreferences.model_validate(self.fetch_preferences())
        company_details = self.fetch_company_details()
        print(company_details)
        filtered_company = {
            key: value for key, value in company_details[0].items() if value is not None
        }
        signals = preferences.preferences.signals
        company_name = company_details[0]["company_name"]
        system_prompt = "You are an outbound SDR who is an expert at research"
        user_prompt = f"""Here are your settings and goals:
        Company you work for: {company_name}
        Your goal: Research target accounts and uncover opportunities or trends about them to use as a reason to reach out through cold emails
        Important Research Points: {signals}
        Research length: 300 words max
        ```
        Analyze the company {company_name} and find insights, trends and signals you can use to write cold emails - {filtered_company}
        ```
        You will proceed by doing the following:
        1.Print 'Opportunities'
        2.Summarize your research in the order of importance - {signals}
        3. Highlight negative trends from the data
        4. Post Final Analysis Summary
        ```
        Begin your analysis."""
        # logger.info(preferences, company_details)
        return system_prompt, user_prompt

    def enrich_company(self):
        system_prompt, user_prompt = self.prompt_creation()
        llm = AIcall()
        insight = llm.openai_chat_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        enrich_response = {"response": insight}
        return enrich_response
