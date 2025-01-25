# <img src="yummy_san/img/logo_processed.jpeg" alt="Logo" width="60" height="60"/> Yummy San

The project uses the capabilities of large language models (LLM) to analyze Yelp reviews and answer the user's questions. The primary use case of this project was to quickly scan Yelp to order the best dish at a restaurant, but can be extended to other use cases such as hotel booking, flights, and many similar use cases.

### Installation

In order to run the project, you will require the following dependencies:

- Python v3.10.14
- Node.js v23.3.0
- npm v10.9.0
- npm-run-all v4.1.5

The backend is written in Python flask, therefore, a python environment needs to be setup. Follow the following steps to create the python environment for the backend:

1. Install anaconda/miniconda on your systesm. Create a virtual environment using the following command:

```bash
$ conda create -n yummy python=3.10.14
$ conda activate yummy
```

2. Install the required python packages using the following command:

```bash
pip install -r flask_project/requirements.txt
```

### Running the project

In order to run the project, you need to run the following commands:

- Run the software using the following command:
   
```bash
$ cd yummy_san && npm run start
```

Open the localhost and enter the Yelp URL for the restaurant you want to analyze. The software will analyze the reviews. The next step is to ask the question and the software will answer the question based on the reviews.


### Future Work

This project is in its early stages and utilizes a quantized large language model (LLM) in the backend to answer the questions. The project can be extended to use a more powerful LLM model to answer the questions.

Currently, the project can be ran on CPU which is efficient for deployment on edge devices. The project can be extended to use GPU for faster processing.

Additionally, the performance of the model can be improved by using the original model instead of the quantized model, provided the hardware support is available.

This project is open for development and contributions. Feel free to contribute to the project.