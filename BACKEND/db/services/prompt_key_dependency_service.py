from db.repository.prompt_key_dependency_repository import PromptKeyDependencyRepository


class PromptKeyDependencyService:

    def __init__(self):
        self.repo = PromptKeyDependencyRepository()


    # CREATE
    def create_dependency(self, prompt_key_id: int, parent_id: int | None, is_parent: bool):
        return self.repo.create(
            prompt_key_id=prompt_key_id,
            parent_id=parent_id,
            is_parent=is_parent
        )


    # GET SINGLE
    def get_dependency(self, dependency_id: int):
        dependency = self.repo.get_by_id(dependency_id)

        if not dependency:
            raise Exception("Dependency not found")

        return dependency


    # GET ALL
    def get_all_dependencies(self):
        return self.repo.get_all()


    # GET BY PROMPT KEY
    def get_dependencies_by_prompt(self, prompt_key_id: int):
        return self.repo.get_by_prompt_key(prompt_key_id)


    # UPDATE
    def update_dependency(self, dependency_id: int, parent_id=None, is_parent=None,uasge_description_dep= None):
        updated = self.repo.update(
            record_id=dependency_id,
            parent_id=parent_id,
            is_parent=is_parent,
            uasge_description_dep = uasge_description_dep
        )

        if not updated:
            raise Exception("Dependency not found")

        return updated


    # DELETE
    def delete_dependency(self, dependency_id: int):
        deleted = self.repo.delete(dependency_id)

        if not deleted:
            raise Exception("Dependency not found")

        return {"message": "Dependency deleted successfully"}
    def get_prompt_dependency_tree(self, start_id: int):
        return self.repo.get_prompt_dependency(start_id)
    
    def get_all_by_parent_id(self,parent_id:int):
        return self.repo.get_all_by_parent_id(parent_id)


prompt_key_dependency_service = PromptKeyDependencyService()