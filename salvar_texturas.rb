# Uso:
#   ruby salvar_texturas.rb "D:/Downloads/sem nome" [pasta_destino]
#
# Varre a pasta (incluindo subpastas), encontra as imagens de texturas
# e copia todas para a pasta de destino (padrão: <pasta>/texturas_salvas).

require 'fileutils'

EXTENSOES = %w[.jpg .jpeg .png .tif .tiff .bmp .tga .webp].freeze

origem = ARGV[0] || 'D:/Downloads/sem nome'
destino = ARGV[1] || File.join(origem, 'texturas_salvas')

abort "Pasta não encontrada: #{origem}" unless Dir.exist?(origem)
FileUtils.mkdir_p(destino)

copiadas = 0
Dir.glob(File.join(origem, '**', '*')).each do |arquivo|
  next unless File.file?(arquivo)
  next unless EXTENSOES.include?(File.extname(arquivo).downcase)
  next if File.expand_path(arquivo).start_with?(File.expand_path(destino))

  nome = File.basename(arquivo)
  alvo = File.join(destino, nome)
  # Evita sobrescrever arquivos com o mesmo nome: acrescenta _1, _2...
  n = 1
  while File.exist?(alvo)
    alvo = File.join(destino, "#{File.basename(nome, '.*')}_#{n}#{File.extname(nome)}")
    n += 1
  end

  FileUtils.cp(arquivo, alvo)
  puts "Salvo: #{alvo}"
  copiadas += 1
end

puts "\n#{copiadas} imagem(ns) salva(s) em #{destino}"
