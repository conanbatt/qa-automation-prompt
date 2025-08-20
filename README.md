# QA Automation Challenge

## Introduction

This challenge is designed to evaluate a candidate’s practical understanding of scripting, databases, and monitoring.

We have an API at https://qa-challenge-nine.vercel.app/api/name-checker that processes names.

This API endpoint has two issues you are expected to find and diagnose accurately.

### Uptime

You are expected to determine the actual service uptime, as expressed in time (% of time the service returns 200) or requests (% of requests that return 200).
To do this, you are expected to build a continuously monitoring script.
In this script, you must log each request into the SQlite database in this project.

Second, you are expected to write a second script that reads from this database, calculates the service uptime, and outputs it to the console.

Tip: Monitoring <10 minutes should be plenty to detect uptime accurately.

### The Bug

There is a bug in this application about the format of names. The API will return a specific error when this happens - you are expected to find out the pattern of this error.

## Deliverable
Create a private fork of this repository and send it over to @conanbatt for review.
Please commit the request_logs database as you store data on it.

You'll need to deliver a reproducible case of the bug, as well as a well-defined uptime number in your deliverable. 

### Tips & Tricks

- It's very important to give your best on this challenge. Please check the [Takehome Guide](https://docs.silver.dev/interview-ready/technical-fundamentals/guia-de-takehomes) to understand what makes an exceptional takehome.
- Bonus points for doing this in Ruby (even if it’s not your main language). Otherwise, python or Javascript is preferred.
- The Bug is not contrived - it does not require lateral thinking.
- You are welcome to use tooling like Postman, but the deliverable must include scripts that execute requests and read from the database.
- Any questions about the challenge, please ask at gabriel@silver.dev.
