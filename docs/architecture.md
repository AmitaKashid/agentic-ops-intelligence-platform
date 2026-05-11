# Architecture

## Overview

The Agentic Operations Intelligence Platform is an enterprise-style backend system for operational ticket triage and incident investigation.

The system receives a user request, classifies the task, selects the required tools, gathers evidence, validates escalation rules, calculates confidence, and returns an evidence-grounded recommendation.

Unlike a traditional RAG chatbot, this platform does not treat every request as a document question. It decides whether the request requires structured metrics, log evidence, policy retrieval, rule validation, or human review.

## High-Level Architecture

```text
Client / User
    |
    v
FastAPI Backend
    |
    v
LangGraph Agent Workflow
    |
    +--> Task Classifier
    |
    +--> Planner
    |
    +--> Tool Router
          |
          +--> SQL Tool
          +--> Log Search Tool
          +--> RAG Tool
          +--> Rule Validator
          +--> Human Review Tool
    |
    +--> Evidence Verifier
    |
    +--> Confidence Scorer
    |
    +--> Response Generator
    |
    +--> Trace Logger
    |
    v
API Response