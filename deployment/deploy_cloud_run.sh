#!/bin/bash
# Script to build & deploy PETCARE INDIA AI to Google Cloud Run and Vertex AI Agent Engine

set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"petcare-india-ai-prod"}
REGION=${GOOGLE_CLOUD_LOCATION:-"asia-south1"}
SERVICE_NAME="petcare-india-ai"

echo "Deploying PetCare India AI to Cloud Run in project: $PROJECT_ID ($REGION)..."

# Build Image via Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,APPLICATION_ENV=production

echo "Deployment finished successfully!"
