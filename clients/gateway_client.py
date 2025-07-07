class MockGatewayClient:
    def analyze_log(self, log: str) -> str:
        return f"Mocked analysis result for log: {log[:60]}..."
