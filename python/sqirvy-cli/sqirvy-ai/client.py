from abc import ABC, abstractmethod


class Client():

#	QueryText(ctx context.Context, system string, prompts []string, model string, options Options) (string, error)

    @abstractmethod
    def QueryText(self, system: str, prompts: list[str], model: str, options: dict[str, str]) -> (str):
        pass

    @abstractmethod
    def Close(self):
        pass
    
    
    
