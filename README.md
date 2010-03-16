
Kokki is a system configuration management framework styled after Chef.

Documentation: http://samuelks.com/kokki/
Source: http://github.com/samuel/kokki
Cookbooks can be found at: http://github.com/samuel/kokki-cookbooks

Q. Why Kokki? Why not Chef or Puppet?

A. Both Chef and Puppet are excellent at what they do. However, what they
   do is not exactly what I'm looking for. Kokki is more of a library for
   configuration management than a system. This is similar to Chef, but
   Kokki goes further in not even trying to provide a client/service part.
   Also, Kokki makes each piece useable by itself. For instance, a recipe
   is just a script that can be run to configure something. The "kokki"
   command just provides a way to group recipes with configurations into
   roles.

Q. Why the name Kokki?

A. Kokki means "cook" in Finnish. The word for Chef is keittiömestari (kitchen master) which is a bit too long for a project name.
