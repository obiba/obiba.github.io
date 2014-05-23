require 'liquid'

module MenuUrlFilter
   def normalize(url, alt)
      if url =~ /http:/
        return url
      end
      return alt.sub(%r{index\.html}i, url)
   end
end

Liquid::Template.register_filter(MenuUrlFilter)