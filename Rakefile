HOME = ENV['HOME']
CWD = File.dirname __FILE__

desc 'Create symlink instead of copying the .dvtcolortheme files'
THEME_FILES = FileList['*.dvtcolortheme']
THEME_DIR = 'Library/Developer/Xcode/UserData/FontAndColorThemes'
directory THEME_DIR
namespace :theme do
  task :install_dvtcolortheme => [THEME_DIR] do |t|
    THEME_FILES.each do |f|
      source = "#{CWD}/#{f}"
      target = "#{HOME}/#{THEME_DIR}/#{f}"
      File.symlink source, target unless File.exists? target
    end
  end
end

task :default => 'theme:install_dvtcolortheme'
