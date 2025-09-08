"""Main CSSMerger API for CSS merging."""

from typing import List, Dict, Optional, Union, Any
from csscade.models import CSSProperty, CSSRule
from csscade.property_merger import PropertyMerger
from csscade.strategies.permanent import PermanentMergeStrategy
from csscade.strategies.component import ComponentMergeStrategy
from csscade.strategies.replace import ReplaceMergeStrategy
from csscade.strategies.base import MergeStrategy


class CSSMerger:
    """
    Main API for CSS merging with multiple strategies.
    
    This is the primary interface for using CSSCade to merge CSS properties
    with intelligent conflict resolution and multiple merge strategies.
    """
    
    def __init__(
        self,
        mode: str = "component",
        conflict_resolution: Optional[Dict[str, str]] = None,
        naming: Optional[Dict[str, Any]] = None,
        validation: Optional[Dict[str, Any]] = None,
        performance: Optional[Dict[str, Any]] = None,
        debug: bool = False
    ):
        """
        Initialize the CSS merger.
        
        Args:
            mode: Merge mode ('permanent', 'component', 'replace')
            conflict_resolution: Conflict resolution configuration
            naming: Class naming configuration
            validation: Validation configuration
            performance: Performance configuration
            debug: Enable debug mode
        """
        self.mode = mode
        self.conflict_resolution = conflict_resolution or {}
        self.naming = naming or {}
        self.validation = validation or {}
        self.performance = performance or {}
        self.debug = debug
        
        # Initialize strategy based on mode
        self._strategy = self._get_strategy(mode)
        
        # Initialize property merger for simple operations
        self._property_merger = PropertyMerger()
    
    def _get_strategy(self, mode: str) -> MergeStrategy:
        """
        Get the appropriate merge strategy based on mode.
        
        Args:
            mode: Merge mode name
            
        Returns:
            Merge strategy instance
        """
        if mode == "permanent":
            return PermanentMergeStrategy(self.conflict_resolution, self.naming)
        elif mode == "component":
            return ComponentMergeStrategy(self.conflict_resolution, self.naming)
        elif mode == "replace":
            return ReplaceMergeStrategy(self.conflict_resolution, self.naming)
        else:
            raise ValueError(f"Unknown merge mode: {mode}")
    
    def merge(
        self,
        source: Union[str, CSSRule, Dict[str, str], List[CSSProperty]],
        override: Union[Dict[str, str], List[CSSProperty], str],
        component_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Merge CSS properties using the configured strategy.
        
        Args:
            source: Source CSS (can be rule, properties, or string)
            override: Override properties
            component_id: Optional component ID for unique naming
            **kwargs: Additional strategy-specific parameters
            
        Returns:
            Dictionary with merge results based on strategy:
                - css: Generated CSS string (optional)
                - add: Classes to add (optional)
                - remove: Classes to remove (optional)
                - preserve: Classes to preserve (optional)
                - inline: Inline styles to apply (optional)
                - important: Important styles to apply (optional)
                - warnings: Warning messages (optional)
                - debug: Debug information (if debug mode enabled)
        """
        # Perform the merge using the selected strategy
        result = self._strategy.merge(
            source=source,
            override=override,
            component_id=component_id,
            **kwargs
        )
        
        # Add debug information if enabled
        if self.debug:
            result["debug"] = {
                "mode": self.mode,
                "strategy": self._strategy.get_strategy_name(),
                "component_id": component_id
            }
        
        return result
    
    def set_mode(self, mode: str) -> None:
        """
        Change the merge mode.
        
        Args:
            mode: New merge mode ('permanent', 'component', 'replace')
        """
        self.mode = mode
        self._strategy = self._get_strategy(mode)
    
    def get_mode(self) -> str:
        """
        Get the current merge mode.
        
        Returns:
            Current merge mode
        """
        return self.mode
    
    def batch(self) -> "BatchMerger":
        """
        Create a batch merger for efficient multiple operations.
        
        Returns:
            BatchMerger instance
        """
        return BatchMerger(self)


class BatchMerger:
    """Handles batch merge operations for efficiency."""
    
    def __init__(self, merger: CSSMerger):
        """
        Initialize batch merger.
        
        Args:
            merger: Parent CSSMerger instance
        """
        self.merger = merger
        self.operations = []
    
    def add(
        self,
        source: Union[str, CSSRule, Dict[str, str], List[CSSProperty]],
        override: Union[Dict[str, str], List[CSSProperty], str],
        component_id: Optional[str] = None,
        **kwargs
    ) -> "BatchMerger":
        """
        Add a merge operation to the batch.
        
        Args:
            source: Source CSS
            override: Override properties
            component_id: Optional component ID
            **kwargs: Additional parameters
            
        Returns:
            Self for chaining
        """
        self.operations.append({
            "source": source,
            "override": override,
            "component_id": component_id,
            "kwargs": kwargs
        })
        return self
    
    def execute(self) -> List[Dict[str, Any]]:
        """
        Execute all batch operations.
        
        Returns:
            List of merge results
        """
        results = []
        for op in self.operations:
            result = self.merger.merge(
                source=op["source"],
                override=op["override"],
                component_id=op.get("component_id"),
                **op.get("kwargs", {})
            )
            results.append(result)
        return results
    
    def clear(self) -> None:
        """Clear all pending operations."""
        self.operations = []