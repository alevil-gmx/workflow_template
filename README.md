# Use Case I - Antibody design

#Intall miniconda for Python3
https://docs.conda.io/en/latest/miniconda.html#linux-installers

# Clone repo  
git clone https://github.com/alevil-gmx/workflow_template.git

# Create conda enviroment with all the dependencies and activate it 
cd workflow_template
conda env create --name use-case1 --file environment.yml
conda activate use-case1

# run jupyter-notebook 

jupyter-notebook workshop-template-ab.ipynb 


