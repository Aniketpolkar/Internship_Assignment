from pymongo import MongoClient
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SecurityAgent")

class SecurityAgent:
    def __init__(self, db_url="mongodb://localhost:27017"):
        self.client = MongoClient(db_url)
        self.db = self.client.auth_db
        self.logs = self.db.security_logs
        self.blocks = self.db.blocked_entities

    def check_access(self, ip: str, email: str = None):
        """Checks if the IP or email is currently blocked."""
        # Check if IP is blocked
        blocked_ip = self.blocks.find_one({"entity": ip, "type": "ip"})
        if blocked_ip:
            if blocked_ip["expiry"] > datetime.utcnow():
                return False, f"IP {ip} is blocked due to: {blocked_ip['reason']}"
            else:
                self.blocks.delete_one({"_id": blocked_ip["_id"]})

        # Check if Email is blocked
        if email:
            blocked_email = self.blocks.find_one({"entity": email, "type": "email"})
            if blocked_email:
                if blocked_email["expiry"] > datetime.utcnow():
                    return False, f"Account {email} is temporarily locked due to: {blocked_email['reason']}"
                else:
                    self.blocks.delete_one({"_id": blocked_email["_id"]})

        return True, "Access granted"

    def log_activity(self, ip: str, email: str, action: str, status: str, details: str = ""):
        """Logs an authentication attempt."""
        log_entry = {
            "timestamp": datetime.utcnow(),
            "ip": ip,
            "email": email,
            "action": action,
            "status": status,
            "details": details
        }
        self.logs.insert_one(log_entry)
        logger.info(f"Logged activity: {action} | IP: {ip} | Email: {email} | Status: {status}")
        
        # Trigger analysis after logging
        self.analyze_and_mitigate(ip, email)

    def analyze_and_mitigate(self, ip: str, email: str):
        """Analyzes recent activity and blocks if suspicious patterns are found."""
        now = datetime.utcnow()
        five_mins_ago = now - timedelta(minutes=5)

        # 1. Brute Force Check (Failed logins per email)
        if email:
            failed_logins = self.logs.count_documents({
                "email": email,
                "action": "login",
                "status": "fail",
                "timestamp": {"$gte": five_mins_ago}
            })
            if failed_logins >= 5:
                self.block_entity(email, "email", "Multiple failed login attempts detected", minutes=15)

        # 2. IP Blocking (Multiple failures from same IP)
        failed_ip_attempts = self.logs.count_documents({
            "ip": ip,
            "status": "fail",
            "timestamp": {"$gte": five_mins_ago}
        })
        if failed_ip_attempts >= 10:
            self.block_entity(ip, "ip", "High volume of suspicious traffic detected", minutes=60)

        # 3. Rapid Registration Check
        registrations = self.logs.count_documents({
            "ip": ip,
            "action": "register",
            "timestamp": {"$gte": now - timedelta(hours=1)}
        })
        if registrations >= 3:
            self.block_entity(ip, "ip", "Too many registrations from this IP", minutes=120)

    def block_entity(self, entity: str, entity_type: str, reason: str, minutes: int):
        """Blocks an IP or email for a specified duration."""
        expiry = datetime.utcnow() + timedelta(minutes=minutes)
        self.blocks.update_one(
            {"entity": entity, "type": entity_type},
            {"$set": {"reason": reason, "expiry": expiry, "blocked_at": datetime.utcnow()}},
            upsert=True
        )
        logger.warning(f"BLOCKED: {entity_type} {entity} for {minutes} mins. Reason: {reason}")

# Singleton instance
security_agent = SecurityAgent()
