> ## Documentation Index
> Fetch the complete documentation index at: https://docs.typesafe.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# TypeSafe Python SDK

> Install the TypeSafe Python SDK and get started with asynchronous or synchronous API calls.

<a id="typesafe-python-sdk" />

Browse the [Python SDK source on GitHub](https://github.com/typesafe-ai/typesafe-sdk-python).

Asynchronous and synchronous Python clients for the [TypeSafe](https://typesafe.ai) API. Learn how to use TypeSafe [here](https://docs.typesafe.ai/).

<h2 id="quickstart">
  Quickstart
</h2>

1. Install the SDK:

   <Tabs>
     <Tab title="uv">
       ```sh theme={null}
       uv add typesafe-sdk
       ```
     </Tab>

     <Tab title="pip">
       ```sh theme={null}
       pip install typesafe-sdk
       ```
     </Tab>
   </Tabs>
2. Set `TYPESAFE_API_KEY` in your environment (create it [here](https://console.typesafe.ai/))
3. Call the System One API:

   <Tabs>
     <Tab title="Async">
       With [AsyncTypeSafeClient](/sdk/python/api/clients/async):

       ```python theme={null}
       from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score


       async def main() -> None:
           async with AsyncTypeSafeClient() as client:
               response = await client.system_one(
                   state={"document": "I was charged twice. Please fix this ASAP."},
                   questions={
                       "billing": Noul(instructions="Is this ticket about billing?"),
                       "tone": Choice(
                           instructions="What is the customer's tone?",
                           criteria={"calm": None, "frustrated": None, "angry": None},
                       ),
                       "urgency": Score(
                           instructions="How urgent is this ticket?",
                           criteria=["can wait", "this week", "today"],
                       ),
                   },
               )

           print(response.nouls["billing"].noul)
           print(response.choices["tone"].choice)
           print(response.scores["urgency"].score)
       ```
     </Tab>

     <Tab title="Sync">
       With [TypeSafeClient](/sdk/python/api/clients/sync):

       ```python theme={null}
       from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

       with TypeSafeClient() as client:
           response = client.system_one(
               state={"document": "I was charged twice. Please fix this ASAP."},
               questions={
                   "billing": Noul(instructions="Is this ticket about billing?"),
                   "tone": Choice(
                       instructions="What is the customer's tone?",
                       criteria={"calm": None, "frustrated": None, "angry": None},
                   ),
                   "urgency": Score(
                       instructions="How urgent is this ticket?",
                       criteria=["can wait", "this week", "today"],
                   ),
               },
           )

       print(response.nouls["billing"].noul)
       print(response.choices["tone"].choice)
       print(response.scores["urgency"].score)
       ```
     </Tab>
   </Tabs>

<h2 id="usage">
  Usage
</h2>

Learn more in the [Usage guide](/sdk/python/usage).
