using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Common.Authentication.DBHandlers
{
    public class SqlQueryer
    {
        /// <summary>
        /// The name of the server that hosts the database. This is
        /// denoted in the connection string by the parameter
        /// "Data Source".
        /// 
        /// TODO: This is not working.
        /// </summary>
        private string DataSource = "localhost:3306";

        /// <summary>
        /// The name of the database that will be queried.
        /// </summary>
        private string InitialCatelog = "auth_central_db";

        /// <summary>
        /// The username of the user trying to make a query to the
        /// database.
        /// </summary>
        private string UserId = "root";

        /// <summary>
        /// The password for the user making a connection.
        /// </summary>
        private string Password = "saline54";

        /// <summary>
        /// The <see cref="SqlConnection"/> object used to query the
        /// database.
        /// </summary>
        private SqlConnection Connection;

        #region Constructors
        /// <summary>
        /// Main constructor for a <see cref="SqlQueryer"/> object.
        /// If testing is true, attributes like <see cref="Connection"/>
        /// will be left null.
        /// </summary>
        /// <param name="testing"></param>
        public SqlQueryer(bool testing=false)
        {
            if (!testing)
            {
                string connectionStr = $"Data Source={DataSource};Initial Catalog={InitialCatelog};User ID={UserId};Password={Password}";
                this.Connection = new SqlConnection(connectionStr);

                this.Initialize();
            }
        }
        #endregion

        #region Connection Management
        /// <summary>
        /// Initialized various attributes for this object.
        /// </summary>
        private void Initialize()
        {
            Connection.Open();
        }
        #endregion

        #region Command Building
        /// <summary>
        /// <para>
        /// Adds the query conditions to the query string. These are
        /// the where conditions in the query that are being added.
        /// The resulting string is returned in the follwing format:
        /// </para>
        /// <para>
        /// {query} WHERE {field1} = {value1}, {field2} = {field2}
        /// </para>
        /// </summary>
        /// <param name="query"></param>
        /// <param name="conditions"></param>
        /// <returns></returns>
        private string WithQueryConditions(string query, Dictionary<string, string> conditions)
        {
            if (conditions.Count > 0)
            {
                string whereConditions = "";
                foreach (string attr in conditions.Keys)
                {
                    string value = conditions[attr];
                    whereConditions = $"{whereConditions} {attr} = {value},";
                }
                whereConditions = whereConditions.Substring(0, whereConditions.Length - 1); // Remove last comma
                query = $"{query} WHERE{whereConditions}";
            }

            return query;
        }

        /// <summary>
        /// Builds the query for a select statement to be called on a database.
        /// The resulting string is returned.
        /// </summary>
        /// <param name="table"></param>
        /// <param name="conditions"></param>
        /// <returns></returns>
        private string BuildSelectStatement(string table, Dictionary<string, string> conditions)
        {
            string command = WithQueryConditions($"SELECT * FROM {table}", conditions) + ";";
            return command;
        }
        #endregion

        #region Queries
        /// <summary>
        /// Queries the database for the given table using the given conditions.
        /// </summary>
        /// <param name="table"></param>
        /// <param name="conditions"></param>
        /// <returns></returns>
        public SqlDataReader Select(string table, Dictionary<string, string> conditions)
        {
            string command = BuildSelectStatement(table, conditions);

            return new SqlCommand(command, Connection).ExecuteReader();
        }
        #endregion
    }
}
