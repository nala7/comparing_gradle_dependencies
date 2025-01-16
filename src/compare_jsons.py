def compare_jsons(json1, json2):
    common_dependencies = []
    for elem in json1:
        if elem in json2:
            common_dependencies.append(elem)


    print(f"Number of common dependencies: {len(common_dependencies)}")

    return common_dependencies