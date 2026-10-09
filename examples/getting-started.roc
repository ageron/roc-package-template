## Replace this example with your own.
app [] {
	pkg: "../package/main.roc",
}

import pkg.Example

main! = |_args| {
	message = Example.greet("World")
	echo!("${message}\n")
	Ok({})
}
