# Project information

## Description

This project is a machine learning project that predicts whether a player is predicted to be banned for botting on Old School Runescape.

### Future public availability
- In future the website will collect data and a new train script will be required.
- At this point the training and datasets for training will be made public.

### Purpose

This project's purpose is only to showcase the machine learning models used for the [Low Latency]('https://low-latency.co.uk)  site.


### Dataset

The model is trained on the top 1k players with the most experience or score in the skill or activity respectively.

The data was recorded over a time period of roughly 3 months and uses the final levels & score of the player and the average daily score and gains for the player.



# Setup
## (N/A) Datasets not yet provided

# Database
The database expects environment variables to be set to get the authentication of the databases.

Your ```~/.bashrc``` would have to contain environment variables like the example:

```shell
export rsLocalHost=""
export rsLocalPort=""
export rsLocalUsername=""
export rsPassword=""
export runescape_database_name=""
```

---

# Running

## Enable MLFlow server
```shell
sh mlflow.sh
```

## Training

```shell
python3 -m training.train
```

## Inference

```shell
python3 -m inference.save_inference
```