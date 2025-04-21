# temporal_worker.py
import asyncio
import concurrent.futures
import traceback
from activities import (
    mcp_call_tool,
    mcp_read_resource,
    mcp_get_prompt,
    mcp_manager,
    invoke_bedrock,
    process_image,
    ingest_data_activity
)
from maap_mcp.mcp_config import TASK_QUEUE, TEMPORAL_HOST, TEMPORAL_PORT
from temporalio.client import Client
from temporalio.worker import Worker
from maap_mcp.logger import logger
from workflows import (
    ImageProcessingWorkflow,
    SemanticCacheCheckWorkflow,
    MemoryRetrievalWorkflow,
    PromptRetrievalWorkflow,
    AIGenerationWorkflow,
    MemoryStorageWorkflow,
    CacheStorageWorkflow,
    DataIngestionWorkflow
)


async def main():
    """Main entry point for the temporal worker."""
    try:
        # Connect to Temporal server
        logger.info(f"Connecting to Temporal server at {TEMPORAL_HOST}:{TEMPORAL_PORT}")
        client = await Client.connect(f"{TEMPORAL_HOST}:{TEMPORAL_PORT}")
        
        # Register workflows and activities
        logger.info(f"Starting worker on task queue {TASK_QUEUE}")
        
        # Create a worker that hosts all workflow implementations and activity implementations
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=100
        ) as activity_executor:
            worker = Worker(
                client,
                task_queue=TASK_QUEUE,
                workflows=[
                    ImageProcessingWorkflow,
                    SemanticCacheCheckWorkflow,
                    MemoryRetrievalWorkflow,
                    PromptRetrievalWorkflow,
                    AIGenerationWorkflow,
                    MemoryStorageWorkflow,
                    CacheStorageWorkflow,
                    DataIngestionWorkflow
                ],
                activities=[
                    mcp_call_tool,
                    mcp_read_resource,
                    mcp_get_prompt,
                    invoke_bedrock,
                    process_image,
                    ingest_data_activity
                ],
                activity_executor=activity_executor,
            )
            # Start listening to task queue
            await logger.ainfo("Temporal worker starting...")
            await worker.run()
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Error in Temporal worker: {str(e)}\n{error_details}")
    finally:
        # Shutdown MCP server connections
        await mcp_manager.shutdown()
    

if __name__ == "__main__":
    asyncio.run(main())