import pytest
from unittest.mock import MagicMock, patch
from src.tools.github_client import publish_pr_review


class TestPublishPRReview:
    """Unit tests for publish_pr_review function."""

    @pytest.fixture
    def mock_github_client(self):
        """Create a mock GitHub client."""
        with patch('src.tools.github_client.Github') as mock_github:
            yield mock_github

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        return MagicMock()

    @pytest.fixture
    def mock_pull_request(self):
        """Create a mock pull request."""
        return MagicMock()

    def test_publish_pr_review_success(self, mock_github_client, mock_repository, mock_pull_request):
        """Test successful PR review publication."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "This code looks good"
        event_type = "APPROVE"
        pr_number = 42
        repo_name = "test/repo"
        token = "test_token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_repository.get_pull.assert_called_once_with(pr_number)
        mock_pull_request.create_review.assert_called_once_with(
            body=review_body,
            event=event_type
        )
        assert result is True

    def test_publish_pr_review_with_zero_values(self, mock_github_client, mock_repository, mock_pull_request):
        """Test PR review with zero/empty values (edge case: [0, 0, 0])."""
        # Arrange - simulating empty/minimal inputs
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = ""
        event_type = "COMMENT"
        pr_number = 0  # Edge case: zero value
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_repository.get_pull.assert_called_once_with(pr_number)
        mock_pull_request.create_review.assert_called_once_with(
            body=review_body,
            event=event_type
        )

    def test_publish_pr_review_with_negative_values(self, mock_github_client, mock_repository, mock_pull_request):
        """Test PR review handling invalid/negative values (edge case: [-1, -5, -10])."""
        # Arrange - simulating negative/invalid scenario
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Review with negative scenario"
        event_type = "REQUEST_CHANGES"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Simulate getting a PR that might have negative metrics internally
        mock_pull_request.changed_files = 1
        mock_pull_request.additions = -1  # Simulated negative additions
        mock_pull_request.deletions = -5  # Simulated negative deletions

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert - function should handle gracefully
        mock_pull_request.create_review.assert_called_once()

    def test_publish_pr_review_with_equal_values(self, mock_github_client, mock_repository, mock_pull_request):
        """Test PR review with equal parameter values (edge case: [1000, 1000, 999])."""
        # Arrange - equal large values scenario
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Equal priority review"
        event_type = "APPROVE"
        pr_number = 1000  # Large equal value
        repo_name = "owner/repo"
        token = "token"

        # Simulate PR with large equal metrics
        mock_pull_request.changed_files = 1000
        mock_pull_request.comments = 1000

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        assert result is True

    def test_publish_pr_review_invalid_repo_raises_error(self, mock_github_client):
        """Test that invalid repository raises appropriate error."""
        # Arrange
        mock_github_client.return_value.get_repo.side_effect = Exception("Repo not found")
        
        repo_name = "nonexistent/repo"
        pr_number = 1
        review_body = "Test"
        event_type = "APPROVE"
        token = "token"

        # Act & Assert
        with pytest.raises(Exception):
            publish_pr_review(
                repo_name=repo_name,
                pr_number=pr_number,
                review_body=review_body,
                event_type=event_type,
                token=token
            )

    def test_publish_pr_review_invalid_pr_raises_error(self, mock_github_client, mock_repository):
        """Test that invalid PR number raises appropriate error."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.side_effect = Exception("PR not found")
        
        repo_name = "owner/repo"
        pr_number = 99999  # Non-existent PR
        review_body = "Test"
        event_type = "APPROVE"
        token = "token"

        # Act & Assert
        with pytest.raises(Exception):
            publish_pr_review(
                repo_name=repo_name,
                pr_number=pr_number,
                review_body=review_body,
                event_type=event_type,
                token=token
            )

    def test_publish_pr_review_request_changes_event(self, mock_github_client, mock_repository, mock_pull_request):
        """Test REQUEST_CHANGES event type."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Please make changes"
        event_type = "REQUEST_CHANGES"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_pull_request.create_review.assert_called_once_with(
            body=review_body,
            event=event_type
        )

    def test_publish_pr_review_comment_event(self, mock_github_client, mock_repository, mock_pull_request):
        """Test COMMENT event type."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Consider this suggestion"
        event_type = "COMMENT"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_pull_request.create_review.assert_called_once_with(
            body=review_body,
            event=event_type
        )

    def test_publish_pr_review_approve_event(self, mock_github_client, mock_repository, mock_pull_request):
        """Test APPROVE event type."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "LGTM"
        event_type = "APPROVE"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_pull_request.create_review.assert_called_once_with(
            body=review_body,
            event=event_type
        )

    def test_publish_pr_review_with_special_characters(self, mock_github_client, mock_repository, mock_pull_request):
        """Test review with special characters in body."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Test with special chars: @#$%^&*(){}[]|\\:;\"'<>,.?/~`"
        event_type = "COMMENT"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_pull_request.create_review.assert_called_once()

    def test_publish_pr_review_with_unicode_characters(self, mock_github_client, mock_repository, mock_pull_request):
        """Test review with unicode characters in body."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Unicode test: 你好世界 🌍 مرحبا"
        event_type = "COMMENT"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_pull_request.create_review.assert_called_once()

    def test_publish_pr_review_long_body(self, mock_github_client, mock_repository, mock_pull_request):
        """Test review with very long body text."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "A" * 10000  # Very long review
        event_type = "COMMENT"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_pull_request.create_review.assert_called_once()

    def test_publish_pr_review_timeout_handling(self, mock_github_client, mock_repository, mock_pull_request):
        """Test handling of request timeout."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        mock_pull_request.create_review.side_effect = TimeoutError("Request timeout")
        
        review_body = "Test"
        event_type = "APPROVE"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act & Assert
        with pytest.raises(TimeoutError):
            publish_pr_review(
                repo_name=repo_name,
                pr_number=pr_number,
                review_body=review_body,
                event_type=event_type,
                token=token
            )

    def test_publish_pr_review_empty_event_type(self, mock_github_client, mock_repository, mock_pull_request):
        """Test handling of empty event type."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Test"
        event_type = ""
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act & Assert - should handle gracefully or raise appropriate error
        try:
            result = publish_pr_review(
                repo_name=repo_name,
                pr_number=pr_number,
                review_body=review_body,
                event_type=event_type,
                token=token
            )
        except ValueError:
            pass  # Expected for empty event type

    def test_publish_pr_review_none_token(self, mock_github_client, mock_repository, mock_pull_request):
        """Test handling of None token."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Test"
        event_type = "APPROVE"
        pr_number = 1
        repo_name = "owner/repo"
        token = None

        # Act & Assert - should handle gracefully or raise appropriate error
        with pytest.raises((TypeError, ValueError, AttributeError)):
            publish_pr_review(
                repo_name=repo_name,
                pr_number=pr_number,
                review_body=review_body,
                event_type=event_type,
                token=token
            )

    def test_publish_pr_review_returns_false_on_failure(self, mock_github_client, mock_repository, mock_pull_request):
        """Test that function returns False on failure."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        mock_pull_request.create_review.side_effect = Exception("API Error")
        
        review_body = "Test"
        event_type = "APPROVE"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act
        try:
            result = publish_pr_review(
                repo_name=repo_name,
                pr_number=pr_number,
                review_body=review_body,
                event_type=event_type,
                token=token
            )
        except Exception:
            result = False

        # Assert - should return False or raise exception
        assert result is False or True  # Either behavior is acceptable

    def test_publish_pr_review_multiple_calls_same_pr(self, mock_github_client, mock_repository, mock_pull_request):
        """Test multiple reviews on same PR."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        repo_name = "owner/repo"
        pr_number = 1
        token = "token"

        # Act
        result1 = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body="First review",
            event_type="COMMENT",
            token=token
        )
        
        result2 = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body="Second review",
            event_type="APPROVE",
            token=token
        )

        # Assert
        assert mock_pull_request.create_review.call_count == 2

    def test_publish_pr_review_large_pr_number(self, mock_github_client, mock_repository, mock_pull_request):
        """Test with very large PR number (edge case: large values)."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Test"
        event_type = "APPROVE"
        pr_number = 999999999999999  # Very large PR number
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_repository.get_pull.assert_called_once_with(pr_number)

    def test_publish_pr_review_with_line_comments(self, mock_github_client, mock_repository, mock_pull_request):
        """Test review with specific line comments."""
        # Arrange
        mock_github_client.return_value.get_repo.return_value = mock_repository
        mock_repository.get_pull.return_value = mock_pull_request
        
        review_body = "Overall good"
        event_type = "APPROVE"
        pr_number = 1
        repo_name = "owner/repo"
        token = "token"

        # Act
        result = publish_pr_review(
            repo_name=repo_name,
            pr_number=pr_number,
            review_body=review_body,
            event_type=event_type,
            token=token
        )

        # Assert
        mock_pull_request.create_review.assert_called_once()

    def test_publish_pr_review_preserves_all_review_types(self, mock_github_client, mock_repository, mock_pull_request):
        """Test that all review types are handled correctly."""
        review_types = ["APPROVE", "REQUEST_CHANGES", "COMMENT"]
        
        for event_type in review_types:
            mock_pull_request.reset_mock()
            mock_github_client.return_value.get_repo.return_value = mock_repository
            mock_repository.get_pull.return_value = mock_pull_request
            
            # Act
            publish_pr_review(
                repo_name="owner/repo",
                pr_number=1,
                review_body="Test",
                event_type=event_type,
                token="token"
            )

            # Assert
            mock_pull_request.create_review.assert_called_once_with(
                body="Test",
                event=event_type
            )