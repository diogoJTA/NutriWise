import scan
import request

class User:
    def __init__(self, age, sex, weight, height, objective = "None", restrictions = "None", diseases = "None"):
        self.assign_parameters(age, sex, weight, height, objective, restrictions)
        self.system_prompt = 'Tu és um ajudante que vai receber uma imagem de um produto ou algo relacionado com nutrição. Tens de ajudar o utilizador com base nas restrições alimentares, objetivo, e tendo como FOCO principal ATENDER as necessidades nutricionais do utilizador. Dá a informação necessárias mas não elabores demasiado e se conciso, a não ser que mesmo necessário. Tens de ser assertivo na tua resposta, e não usar "talvez", "é possível que", etc., tendo com cuidado na mesma que cada pessoa é diferente. Responde APENAS em Português de Portugal!'
        self.update_user_prompt()

    def assign_parameters(self, age, sex, weight, height, objective, restrictions):
        self.user_info_dic = {}
        self.user_info_dic["age"] = age
        self.user_info_dic["sex"] = sex
        self.user_info_dic["weight"] = weight
        self.user_info_dic["height"] = height
        self.user_info_dic["objective"] = objective
        self.user_info_dic["restrictions"] = restrictions
        self.update_user_prompt()
    
    def update_user_prompt(self):
        user_prompt = ""
        for i, (key, value) in enumerate(self.user_info_dic.items()):
            user_prompt += f"{i}: {key} => {value}\n"
        self.user_prompt = user_prompt
        
    def agent_answer(self, imag_path, usepaddle=True):
        if(usepaddle == True):
            paddle_prompt = scan.scan_text(imag_path)
        else:
            paddle_prompt = "(Not working)"
        user_prompt = self.user_prompt
        system_prompt = self.system_prompt
        answer = request.analyse_product(system_prompt, user_prompt, paddle_prompt, imag_path)
        return answer

if __name__ == "__main__":
    user = User("20", "Male", "70Kg", "170cm", "Gain muscle and get buffed", "intolerant to gluten", "diabetis")

    print(user.agent_answer("fanta.jpg", usepaddle=False))



