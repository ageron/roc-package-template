## Replace this module with your package's public API.
Example :: {}.{

	## Return a greeting for the given name.
	greet : Str -> Str
	greet = |name| "Hello, ${name}!"
}

## Your private functions and types go here.

## Your module tests go here.

expect Example.greet("Roc") == "Hello, Roc!"
expect Example.greet("") == "Hello, !"
