import json
import requests 

MISTRAL_API_KEY = '<insert mistral API here>'
RADIO_FRANCE_API_KEY = "<insert radio france API token here>"
GRAPHQL_URL = f"https://openapi.radiofrance.fr/v1/graphql?x-token={RADIO_FRANCE_API_KEY}"

def download_schema():
    url = GRAPHQL_URL
    params = {'x-token': RADIO_FRANCE_API_KEY}
    headers = {'x-token': RADIO_FRANCE_API_KEY}
    body = """ 
    query {
    __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
        ...FullType
        }
        directives {
        name
        description
        locations
        args {
            ...InputValue
        }
        }
    }
    }

    fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
        name
        description
        args {
        ...InputValue
        }
        type {
        ...TypeRef
        }
        isDeprecated
        deprecationReason
    }
    inputFields {
        ...InputValue
    }
    interfaces {
        ...TypeRef
    }
    enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
    }
    possibleTypes {
        ...TypeRef
    }
    }

    fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
    }

    fragment TypeRef on __Type {
    kind
    name
    ofType {
        kind
        name
        ofType {
        kind
        name
        ofType {
            kind
            name
        }
        }
    }
    }
    """
    response = requests.post(url=url, json={"query": body}, params=params, headers=headers) 
    if response.status_code == 200: 
        # print(json.dumps(json.loads(response.content), indent=2))
        return json.loads(response.content)
    else:
        return None
    

# TODO: fix following methods

def generate_query_function(query_name, query_args):
    def query_func(*args, **kwargs):
        # Construct the GraphQL query
        query = f"query {{ {query_name}({query_args}) {{ __typename }} }} }}"

        # Send the query to the GraphQL server
        response = requests.post(url=GRAPHQL_URL, json={"query": query}, params=params, headers=headers)

        if response.status_code == 200:
            # Extract the result from the response
            result = response.json()["data"][query_name]

            # Convert the result to a string and return it
            return json.dumps(result)
        else:
            return None

    return query_func

def generate_mutation_function(mutation_name, mutation_args):
    def mutation_func(*args, **kwargs):
        # Construct the GraphQL mutation
        mutation = f"mutation {{ {mutation_name}({mutation_args}) {{ __typename }} }} }}"

        # Send the mutation to the GraphQL server
        response = requests.post(url=GRAPHQL_URL, json={"query": mutation}, params=params, headers=headers)

        if response.status_code == 200:
            # Extract the result from the response
            result = response.json()["data"][mutation_name]

            # Convert the result to a string and return it
            return json.dumps(result)
        else:
            return None

    return mutation_func

def generate_query_function(query_name, query_args):
    def query_func(*args, **kwargs):
        # Construct the GraphQL query
        query = f"query {{ {query_name}({query_args}) {{ __typename }} }} }}"

        # Send the query to the GraphQL server
        response = requests.post(url=GRAPHQL_URL, json={"query": query}, params=params, headers=headers)

        if response.status_code == 200:
            # Extract the result from the response
            result = response.json()["data"][query_name]

            # Convert the result to a string and return it
            return json.dumps(result)
        else:
            return None

    return query_func

def generate_mutation_function(mutation_name, mutation_args):
    def mutation_func(*args, **kwargs):
        # Construct the GraphQL mutation
        mutation = f"mutation {{ {mutation_name}({mutation_args}) {{ __typename }} }} }}"

        # Send the mutation to the GraphQL server
        response = requests.post(url=GRAPHQL_URL, json={"query": mutation}, params=params, headers=headers)

        if response.status_code == 200:
            # Extract the result from the response
            result = response.json()["data"][mutation_name]

            # Convert the result to a string and return it
            return json.dumps(result)
        else:
            return None

    return mutation_func

def generate_tools_functions(schema):
    tools_functions = {}

    # Generate query functions
    for query_type in schema["data"]["__schema"]["queryType"]["fields"]:
        if query_type["name"] != "__typename":
            query_name = query_type["name"]
            query_args = ", ".join([f"${{arguments.{arg_name}: {arg_type}}}}}" for arg_name, arg_type in query_type["args"].items()])
            query_func = generate_query_function(query_name, query_args)
            tools_functions[query_name] = {
                "function": query_func,
                "arguments": {arg_name: {"type": arg_type} for arg_name, arg_type in query_type["args"].items()}
            }

    # Generate mutation functions
    for mutation_type in schema["data"]["__schema"]["mutationType"]["fields"]:
        if mutation_type["name"] != "__typename":
            mutation_name = mutation_type["name"]
            mutation_args = ", ".join([f"${{arguments.{arg_name}: {arg_type}}}}}" for arg_name, arg_type in mutation_type["args"].items()])
            mutation_func = generate_mutation_function(mutation_name, mutation_args)
            tools_functions[mutation_name] = {
                "function": mutation_func,
                "arguments": {arg_name: {"type": arg_type} for arg_name, arg_type in mutation_type["args"].items()}
            }

    return tools_functions

schema = download_schema()
tools_functions = generate_tools_functions(schema)
print(tools_functions)