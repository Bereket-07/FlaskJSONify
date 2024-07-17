
# prompt = prompt_template.format(
#     title=processed_data["title"],
#     description=processed_data["description"],
#     topic=processed_data["topic"],
#     total_audience=processed_data["total_audience"],
#     questions_and_answers=formatted_qa,
#     language="English",
# )

# store = {}

# model = ChatGroq(model="llama3-8b-8192")
# chain = prompt_template | model

# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]

# config = {"configurable": {"session_id": "abc4"}}

# # with_message_history = RunnableWithMessageHistory(
# #     chain,
# #     get_session_history,
# #     input_messages_key="messages",
# # )

# # response = chain.invoke(
# #     [HumanMessage(content="hii i am bereket")],
# #     config=config
# # )
# # print(response.content)
