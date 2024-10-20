import chromadb
import psutil
import logging
import time

from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='chroma_diagnostics.log'
)

class ChromaHealthCheck:
    def __init__(self, persist_directory="./chroma_storage"):
        self.persist_directory = persist_directory
        self.client = None
        
    def connect_with_monitoring(self):
        """Attempt to connect to ChromaDB with resource monitoring"""
        try:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            logging.info("Successfully connected to ChromaDB")
            return True
        except Exception as e:
            logging.error(f"Connection failed: {str(e)}")
            return False
    
    def monitor_resources(self, duration=60):
        """Monitor system resources for a specified duration"""
        start_time = time.time()
        metrics = []
        
        while time.time() - start_time < duration:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(self.persist_directory)
            
            metrics.append({
                'timestamp': datetime.now(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
                'memory_available': memory.available / (1024 * 1024 * 1024),  # GB
                'disk_available': disk.free / (1024 * 1024 * 1024)  # GB
            })
            
            logging.info(f"CPU: {cpu_percent}% | Memory: {memory.percent}% | Disk: {disk.percent}%")
            
            if memory.percent > 90 or disk.percent > 90:
                logging.warning("Resource usage critically high!")
            
            time.sleep(5)
        
        return metrics
    
    def check_thread_integrity(self):
        """Verify thread data integrity in ChromaDB"""
        try:
            collections = self.client.list_collections()
            for collection in collections:
                count = collection.count()
                logging.info(f"Collection {collection.name}: {count} documents")
                
                # Sample a few documents to verify accessibility
                if count > 0:
                    try:
                        sample = collection.get(limit=1)
                        logging.info("Successfully retrieved sample document")
                    except Exception as e:
                        logging.error(f"Failed to retrieve documents: {str(e)}")
                        
        except Exception as e:
            logging.error(f"Failed to check thread integrity: {str(e)}")
    
    def run_diagnostics(self):
        """Run complete diagnostic check"""
        logging.info("Starting ChromaDB diagnostics...")
        
        # Connection check
        if not self.connect_with_monitoring():
            return "Failed to connect to ChromaDB"
        
        # Check disk permissions
        try:
            with open(f"{self.persist_directory}/test_write.tmp", 'w') as f:
                f.write("test")
            import os
            os.remove(f"{self.persist_directory}/test_write.tmp")
            logging.info("Disk permissions check passed")
        except Exception as e:
            logging.error(f"Disk permission error: {str(e)}")
            return "Failed disk permissions check"
        
        # Monitor resources
        metrics = self.monitor_resources(duration=30)  # Monitor for 30 seconds
        
        # Check thread integrity
        self.check_thread_integrity()
        
        return {
            "status": "completed",
            "metrics": metrics,
            "collections_status": "verified" if self.client else "not_checked"
        }

def main():
    checker = ChromaHealthCheck()
    results = checker.run_diagnostics()
    logging.info(f"Diagnostic results: {results}")

if __name__ == "__main__":
    main()
