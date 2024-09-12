from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

runnable = RunnableParallel(
    origin=RunnablePassthrough(),
    modified=lambda x: x+1
)

res = runnable.invoke(1) # {'origin': 1, 'modified': 2}
print(res)


def fake_llm(prompt: str) -> str: # Fake LLM for the example
    return "completion"

chain = RunnableLambda(fake_llm) | {
    'original': RunnablePassthrough(), # Original LLM output
    'parsed': lambda text: text[::-1] # Parsing logic
}

res = chain.invoke('hello') # {'original': 'completion', 'parsed': 'noitelpmoc'}
print(res)
