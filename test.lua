-- Configuração básica de inventário
local inventario = {}

-- Função para adicionar itens ao inventário
function adicionarItem(nome, quantidade)
    if inventario[nome] then
        inventario[nome] = inventario[nome] + quantidade
    else
        inventario[nome] = quantidade
    end
    print(nome .. " adicionado. Quantidade: " .. inventario[nome])
end

-- Função para remover itens do inventário
function removerItem(nome, quantidade)
    if inventario[nome] then
        if inventario[nome] >= quantidade then
            inventario[nome] = inventario[nome] - quantidade
            print(nome .. " removido. Quantidade restante: " .. inventario[nome])
            if inventario[nome] == 0 then
                inventario[nome] = nil
            end
        else
            print("Quantidade insuficiente de " .. nome .. " para remover.")
        end
    else
        print(nome .. " não encontrado no inventário.")
    end
end

-- Função para listar itens do inventário
function listarInventario()
    print("Inventário:")
    for nome, quantidade in pairs(inventario) do
        print(nome .. ": " .. quantidade)
    end
end

-- Exemplo de uso
adicionarItem("Espada", 1)
adicionarItem("Poção", 5)
removerItem("Poção", 2)
listarInventario()