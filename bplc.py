#! python3

import os
import sys

if len(sys.argv) >= 2:
	n = 1
	sysb = sysa = []
	aparams = bparams = str()
	help = execute = pause = cmdln = uparam = nologo = False
	exename = intname = savefinal = savecmdln = nofiles = None

	for v in sys.argv:
		if v == "-h":
			print("Use \"bplc [parameters] filename\" to launch.\n\n\tfilename\tName of file\n\nList of parameters:\n\n\t-e\tExecute filename.exe file if exists (helpful for compiled language)\n\t-p\tPause after execution script\n\t-c\tPrint execution command\n\t-nl\tHide logo\n\t-nf\tExecute script without file (need -i)\n\t-sf\tCreate .bat file for further executions\n\t-sc\tCreate .bplc.bat with execution command line for BPLC\n\t-i(...)\tUse specified interpreter (compiler) like -i(interpreter) or -i(interpreter.exe)\n\t-e(...)\tExecute specified file like -e(filename) or -e(filename.exe)\n\t-sf(...)\tCreate specified file for further executions like -sf(filename) or -sf(filename.bat)\n\t-sc(...)\tCreate specified file with execution command line for BPLC\n\t-nf(...)\tSpecified name for command without file (need for -sf and -sc)\n\t-pb\tAdd parameter before filename in execute command like -pb(-c)\n\t-pa\tAdd parameter after filename in execute command like -pa(-c)\n\t-eb\tExecute command before execute interpreter (compiler) like -eb(make)\n\t-ea\tExecute command after execute interpreter (compiler) like -ea(make)")
			help = True
			break
		elif v == "-e":
			execute = True
			n += 1
		elif v == "-p":
			pause = True
			n += 1
		elif v == "-c":
			cmdln = True
			n += 1
		elif v == "-nl":
			nologo = True
			n += 1
		elif v == "-nf":
			nofiles = "_NO_NAME_"
			n += 1
		elif v == "-sf":
			savefinal = "?"
			n += 1
		elif v == "-sc":
			savecmdln = "?"
			n += 1
		elif v[:3] == "-i(":
			intname = v[3:v.find(")")]
			n += 1
		elif v[:3] == "-e(":
			exename = v[3:v.find(")")]
			execute = True
			n += 1
		elif v[:4] == "-sf(":
			savefinal = v[4:v.find(")")]
			n += 1
		elif v[:4] == "-sc(":
			savecmdln = v[4:v.find(")")]
			n += 1
		elif v[:4] == "-nf(":
			nofiles = v[4:v.find(")")]
			n += 1
		elif v[:4] == "-pb(":
			bparams += " " + v[4:v.find(")")]
			n += 1
		elif v[:4] == "-pa(":
			aparams += " " + v[4:v.find(")")]
			n += 1
		elif v[:4] == "-eb(":
			sysb.append(v[4:v.find(")")])
			n += 1
		elif v[:4] == "-ea(":
			sysa.append(v[4:v.find(")")])
			n += 1
		else:
			if v != sys.argv[0] and not os.path.exists(v):
				print("BPLC: Unknown parameter \"" + v + "\"!")
				uparam = True
				break

	if not help:
		if not nologo:
			print("BPLC v1.6.5 public")

		if (len(sys.argv) > n or nofiles) and not uparam:
			if len(sys.argv) > n and nofiles:
				print("BPLC: Not parameterized files are ignored!")

			canDo = True
			saveStr = str()
			files, curext = sys.argv[n] if not nofiles else str(), os.path.splitext(sys.argv[n])[1] if not nofiles else str()

			if not nofiles:
				for i in range(n + 1, len(sys.argv)):
					if os.path.splitext(sys.argv[i])[1] == curext and os.path.exists(sys.argv[i]):
						files += " " + sys.argv[i]
					else:
						canDo = False
						break

			if canDo:
				intrepts = {
					".c": "dmc",
					".clj": "clojure.bat",
					".coffee": "coffee",
					".cpp": "dmc",
					".cs": "csc",
					".d": "dmd",
					".dart": "dart",
					".erl": "erl",
					".fs": "fsc",
					".go": "go",
					".hs": "runhaskell",
					".lua": "lua",
					".n": "ncc",
					".js": "node",
					".pl": "perl",
					".php": "php",
					".py": "python",
					".r": "r"
				}

				intrept = intrepts.get(curext) if not intname else intname

				if intrept:
					basefilename = os.path.basename(sys.argv[n]).split(os.path.splitext(sys.argv[n])[1])[0] if not nofiles else nofiles
					exefile = exename if exename else basefilename + ".exe"

					if savefinal == "?":
						savefinal = basefilename

					if savecmdln == "?":
						savecmdln = basefilename + ".bplc"

					if os.path.exists(exefile):
						os.remove(exefile)

					rstr = (intrept + bparams + " " + files + aparams).strip()

					if cmdln:
						print("BPLC: Command line: " + rstr)

					for v in sysb:
						if cmdln:
							print("BPLC: Command line: " + v)

						os.system(v)

						if savefinal:
							saveStr += v + "\n"

					os.system(rstr)

					if savefinal:
						saveStr += rstr + "\n"

					for v in sysa:
						if cmdln:
							print("BPLC: Command line: " + v)

						os.system(v)

						if savefinal:
							saveStr += v + "\n"

					if execute:
						if os.path.exists(exefile):
							if savefinal and len(saveStr) > 0:
								saveStr += exefile + "\n"

							os.system(exefile)
						else:
							print("BPLC: Execution file not found!")
				else:
					print("BPLC: " + "Extension not found!" if not nofiles else "Not found -i(...) parameter!")
			else:
				print("BPLC: Error in extension of one or more files!")

			if pause:
				if savefinal and len(saveStr) > 0:
					saveStr += "pause\n"

				os.system("pause")

			if savecmdln or savefinal:
				if savecmdln != savefinal:
					if savecmdln != None:
						wfile = open(savecmdln + ".bat", "w")
						wfile.write("@echo off\nbplc")

						for v in sys.argv:
							if v != sys.argv[0] and v[:3] != "-sc" and v[:3] != "-sf":
								wfile.write(" " + v)

						wfile.close()

					if len(saveStr) > 0:
						wfile = open(savefinal + ".bat", "w")
						wfile.write("@echo off\n")
						wfile.write(saveStr.strip())
						wfile.close()
				else:
					print("BPLC: Save files have the same name!")
		else:
			if not uparam:
				print("BPLC: File(s) not found!")
else:
	print("BPLC: Parameters not found!")