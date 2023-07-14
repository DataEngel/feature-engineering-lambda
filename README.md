## Feature engineering lambda

* **Description:** Lambda that reads a csv file from an s3 bucket, does the feature engineering processing, and persists the output to an s3 bucket once it's done. 

* **Input:** It doesn't need a payload, it just takes an input trigger of any kind, from a python api or aws api gateway, etc. 

* **Output:** It doesn't return a json to anything like that, what happens at the end is that it persists the output to an s3 ticket. 

### Architecture

![Architecture](https://github.com/DataEngel/inference-lambda/assets/63415652/9e71f83c-0b4f-48d4-82d6-87bbbb60245c)
