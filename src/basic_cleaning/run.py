#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    df = pd.read_csv(artifact_local_path)
    logger.info("Successfully read in file")

    idx = df['price'].between(args.min_price, args.max_price)
    logger.info("Removed outliers")

    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
    args.output_artifact,
    type=args.output_type,
    description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

    logger.info("Saved cleaned data artifact to W&B")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str, 
        help='name of input artifact to be cleaned', 
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str, 
        help='name of output artifact', 
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help='type of output artifact',
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help='description of output artifact',
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help='values below this are considered outliers',
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help='values above this are considered outliers',
        required=True
    )


    args = parser.parse_args()

    go(args)
