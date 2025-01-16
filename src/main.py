from repo import Repo
from gradle_dependencies_to_json import gradle_to_json
from compare_jsons import compare_jsons
import os

separator_string = "-------------------------------"




base_dir = os.path.abspath(os.getcwd())
print(base_dir)

besu = Repo("Besu", "https://github.com/hyperledger/besu", base_dir, gitoken)
besu_json = gradle_to_json(besu.local_repo_dir)
print(f"Number of dependencies in Besu {len(besu_json)}")


teku = Repo("Teku", "https://github.com/Consensys/teku", base_dir,  gitoken)
teku_json = gradle_to_json(teku.local_repo_dir)
print(f"Number of dependencies in Teku {len(teku_json)}")

print(besu.local_repo_dir)
print(teku.local_repo_dir)
compare_jsons(besu_json, teku_json)
