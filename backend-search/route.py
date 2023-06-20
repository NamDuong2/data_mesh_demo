"""Routing."""
from flask import  (
    Flask,
    render_template
)
from form import DataProductForm
from api.elastic_test import connect_elasticsearch
from github import Github
from config.config_handling import get_config_value

# Retrieve secret variable 
_secret_key = get_config_value('flask', 'secret_key')
_access_token = get_config_value("github", "access_token")
_github_repo_path = get_config_value("github", "repo_path")
_search_ui_url = get_config_value("elastic-search-ui", "search_ui_url")

app = Flask(__name__, instance_relative_config=False, template_folder='templates')
app.config['SECRET_KEY'] = _secret_key

# Initiate Elasticsearch connector object 
try:
    es = connect_elasticsearch()
except:
    print("Connect to Elastic failed!!!")

# Check if index existed
_index_name = get_config_value("elastic", "es_index")
if es.indices.exists(index=_index_name) == False:
    print(f"Index {_index_name} does not exist.")
    print(f"Creating a new one with name: {_index_name}...")
    es.indices.create(index=_index_name)
    print("Created successfully!!!")
else:
    print(f"Index {_index_name} existed")

@app.route("/register_dp", methods=["GET", "POST"])
def data_product():
    """Standard `Data Product` form."""
    form = DataProductForm()
    print("1")
    if form.validate_on_submit():
        print("2")
        # retrieve data from form
        data_prod_name = form.data_prod_name.data
        tags = form.tags.data
        data_prod_owner = form.data_prod_owner.data
        data_prod_owner_contact = form.data_prod_owner_contact.data
        res_tech_team = form.res_tech_team.data
        tech_support_contact = form.tech_support_contact.data
        business_unit = form.business_unit.data
        data_prod_business_description = form.data_prod_business_description.data

        # Public Web Github using an access token
        g = Github(_access_token)
        repo = g.get_repo(_github_repo_path)
        # create empty description file for particular data product
        repo.create_file(f"{data_prod_name}/{data_prod_name}_description.md", "", "")

        # return project_url (github url data product for user to upload)
        encode_dp_name = data_prod_name.replace(" ", "%20")
        project_url = f"https://github.com/{_github_repo_path}/tree/main/{encode_dp_name}"
        # write user input data to Elasticsearch
        
        data_prod_object = {
            'data_prod_name': data_prod_name,
            'tags': tags,
            'data_prod_owner': data_prod_owner,
            'data_prod_owner_contact': data_prod_owner_contact,
            'res_tech_team': res_tech_team,
            'tech_support_contact': tech_support_contact,
            'business_unit': business_unit,
            'data_prod_business_description': data_prod_business_description,
            'project_url': project_url
        }
        es.index(index=_index_name, document=data_prod_object)
        return render_template("submit_success.html", 
                               project_url = project_url, 
                               data_prod_name = data_prod_name,
                               search_ui_url = _search_ui_url)
    return render_template(
        "data_product.html", form=form, template="form-template", title="Data Product Form"
    )

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)