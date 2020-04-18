using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Scripting.Hosting;
using IronPython.Hosting;
using System.Linq.Expressions;
using System.Data;

namespace MDO_IronPython
{
    public static class ModMethod
    {
        private static ScriptSource methodSource;
        private static ScriptScope methodScope;
        private static ScriptEngine engine;
        static ModMethod()
        {
            var resourceName = "MDO_IronPython.res.modMet.ModMethodFull.py";
            string pySrc;

            using (var stream = System.Reflection.Assembly.GetExecutingAssembly()
                                      .GetManifestResourceStream(resourceName))
            using (var reader = new System.IO.StreamReader(stream))
            {
                pySrc = reader.ReadToEnd();
            }
            ModMethod.engine = Python.CreateEngine();
            var x = ModMethod.engine.CreateScriptSourceFromString(pySrc);
            ModMethod.methodSource = x;
            ModMethod.methodScope = x.Engine.CreateScope();
            x.Execute(ModMethod.methodScope);
        }
        private static (dynamic OptimizingFunction, dynamic lipzitsFunction) getFunctionsVariables(string optFuncPyCode,string funcName, string lipFuncPyCode,string lipFuncName)
        {
            var optFuncScriptSource = ModMethod.engine.CreateScriptSourceFromString(optFuncPyCode);
            var optFuncScope = optFuncScriptSource.Engine.CreateScope();

            var lipFuncScriptSource = ModMethod.engine.CreateScriptSourceFromString(optFuncPyCode);
            var lipFuncScope = lipFuncScriptSource.Engine.CreateScope();

            optFuncScriptSource.Execute(optFuncScope);
            lipFuncScriptSource.Execute(lipFuncScope);

            dynamic opf = optFuncScope.GetVariable(funcName);
            dynamic lipf = lipFuncScope.GetVariable(lipFuncName);
            return (opf, lipf);
        }

        public static dynamic solve(string optFuncText,string optFuncName, string lipFuncText,string lipFuncName, double precision, double epsilon, double[] lower, double[] upper, int ruleSubList, int ruleMainList)
        {
            dynamic solveFunc = ModMethod.methodScope.GetVariable("solve");
            var funcs = getFunctionsVariables(optFuncText, optFuncName, lipFuncText,lipFuncName);
            dynamic result = solveFunc(funcs.OptimizingFunction, funcs.lipzitsFunction,precision,epsilon,lower,upper,ruleSubList,ruleMainList);
            return result;
        }
    }
}
