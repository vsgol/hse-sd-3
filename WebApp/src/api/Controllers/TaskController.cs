using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using logic.Models;
using data_lib;

namespace api.Controllers;

[Route("api/[controller]")]
[ApiController]
public class TaskController : Controller
{
    private readonly HwDbContext _context;
    
    public TaskController(HwDbContext context)
    {
        _context = context;
    }
    
    // GET: api/Task
    [HttpGet]
    public async Task<ActionResult<IEnumerable<HwTask>>> GetTasks()
    {
        return await _context.Tasks.ToListAsync();
    }
    
    // GET: api/Task/1
    [HttpGet("{id}")]
    public async Task<ActionResult<HwTask>> GetTask(int id)
    {
        var task = await _context.Tasks.FindAsync(id);

        if (task == null)
        {
            return NotFound();
        }

        return task;
    }
    
    // PUT: api/Task/1
    [HttpPut("{id}")]
    public async Task<IActionResult> PutTask(int id, HwTask task)
    {
        if (id != task.Id)
        {
            return BadRequest();
        }

        _context.Entry(task).State = EntityState.Modified;

        try
        {
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException)
        {
            if (!TaskExists(id))
            {
                return NotFound();
            }
            else
            {
                throw;
            }
        }

        return NoContent();
    }

    // POST: api/Task
    [HttpPost]
    public async Task<ActionResult<HwTask>> PostTask(HwTask task)
    {
        _context.Tasks.Add(task);
        await _context.SaveChangesAsync();

        return CreatedAtAction("GetTask", new { id = task.Id }, task);
    }

    // DELETE: api/Task/1
    [HttpDelete("{id}")]
    public async Task<ActionResult<HwTask>> DeleteTask(int id)
    {
        var task = await _context.Tasks.FindAsync(id);
        if (task == null)
        {
            return NotFound();
        }
        
        foreach (var attempt in _context.Attempts.Where(a => a.TaskId == task.Id).ToList())
        {
            AttemptController.DeleteAttempt(_context, attempt);
        }
        
        _context.Tasks.Remove(task);
        await _context.SaveChangesAsync();

        return task;
    }

    private bool TaskExists(int id)
    {
        return _context.Tasks.Any(e => e.Id == id);
    }
}