tree -a -I '.git|.vscode|__pycache__|*.log|static|static_cdn|deployment|.local|media' > dir.tree
sed -i 's/  /  /g' dir.tree
pipenv graph > graph.txt

isort $@
black $@ --line-length 120
flake8 $@ --max-line-length 120 --exclude=__init__.py,settings
