# AWS Deployment Notes

## Serverless default
- **Frontend**: S3 + CloudFront
- **Backend**: API Gateway + Lambda (FastAPI via Mangum)
- **Database**: RDS Postgres or Aurora Serverless v2
- **Scheduler**: EventBridge monthly trigger for crawler

## Backend (SAM)
1. Install AWS SAM CLI.
2. Package and deploy:
   - `sam build`
   - `sam deploy --guided`

## Frontend (S3 + CloudFront)
1. Build web app: `npm run build`
2. Upload `web/dist/` to S3.
3. Point CloudFront to the S3 bucket and enable HTTPS.

## Scheduler
Use EventBridge rule to invoke the crawler Lambda monthly.
