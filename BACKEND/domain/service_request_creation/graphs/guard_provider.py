from llm.utils.guardrails_utils import GuardrailsUtils
from domain.service_request_creation.graphs.state_schemas import ClassificationResult,MandatoryExtractionResult,FinalSummary

class SRGuardProvider:
    def __init__(self):
        self._classification_guard = GuardrailsUtils.create_guard(ClassificationResult)
        self._madatory_fields_guard = GuardrailsUtils.create_guard(MandatoryExtractionResult)
        self.final_summary_guard = GuardrailsUtils.create_guard(FinalSummary)

    def validate_classification(self, llm_output: str) -> ClassificationResult:
        try:
            if not llm_output:
                raise ValueError("Empty LLM output")
    
            outcome = self._classification_guard.parse(llm_output)
    
            if outcome.validation_passed:
                return GuardrailsUtils.map_to_schema(ClassificationResult,outcome.validated_output)

    
        except Exception:
            pass
        
        # 🔥 fallback (empty result)
        return ClassificationResult(
            service=None,
            request_type=None
        )

    def validate_mandatory_fields(self, llm_output: str) -> MandatoryExtractionResult:
        try:
            if not llm_output:
                raise ValueError("Empty LLM output")
    
            outcome = self._madatory_fields_guard.parse(llm_output)
    
            if outcome.validation_passed:
                return GuardrailsUtils.map_to_schema(MandatoryExtractionResult,outcome.validated_output)
    
        except Exception:
            pass
        
        # 🔥 fallback (empty result)
        return MandatoryExtractionResult(
        )
    def validate_final_summary(self, llm_output: str) -> FinalSummary:
        try:
            if not llm_output:
                raise ValueError("Empty LLM output")
    
            outcome = self.final_summary_guard.parse(llm_output)
    
            if outcome.validation_passed:
                return GuardrailsUtils.map_to_schema(FinalSummary,outcome.validated_output)
    
        except Exception:
            pass
        
        # 🔥 fallback (empty result)
        return FinalSummary( final_summary=""
        )